from flask import Blueprint, request, jsonify
from extensions import db
from models import Request, Item, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

request_bp = Blueprint('requests', __name__, url_prefix='/api/requests')

@request_bp.route('/item/<int:item_id>', methods=['POST'])
@jwt_required()
def create_request(item_id):
    """
    Create a new request for an item (seeker requests an item)
    Expected JSON:
    {
        "message": "I really need this sofa for my new house..."
    }
    """
    try:
        data = request.get_json()
        seeker_id = get_jwt_identity()
        
        # Validate message
        if not data or 'message' not in data or not data['message']:
            return jsonify({'error': 'Please explain why you need this item'}), 400
        
        # Check if item exists and is available
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        if not item.is_available:
            return jsonify({'error': 'This item is no longer available'}), 400
        
        # Check if user is trying to request their own item
        if item.giver_id == int(seeker_id):
            return jsonify({'error': 'You cannot request your own item'}), 400
        
        # Check if user already has a pending request for this item
        existing_request = Request.query.filter_by(
            item_id=item_id,
            seeker_id=seeker_id,
            status='pending'
        ).first()
        
        if existing_request:
            return jsonify({'error': 'You already have a pending request for this item'}), 400
        
        # Create new request
        new_request = Request(
            message=data['message'],
            status='pending',
            seeker_id=int(seeker_id),
            item_id=item_id
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Request sent successfully',
            'request': new_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@request_bp.route('/incoming', methods=['GET'])
@jwt_required()
def get_incoming_requests():
    """
    Get all requests for items that the current user is giving away
    """
    try:
        user_id = get_jwt_identity()
        
        # Find all items posted by this user
        user_items = Item.query.filter_by(giver_id=user_id).all()
        item_ids = [item.id for item in user_items]
        
        # Get all requests for those items
        requests = Request.query.filter(Request.item_id.in_(item_ids)).order_by(Request.created_at.desc()).all()
        
        return jsonify([req.to_dict() for req in requests]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@request_bp.route('/outgoing', methods=['GET'])
@jwt_required()
def get_outgoing_requests():
    """
    Get all requests made by the current user
    """
    try:
        user_id = get_jwt_identity()
        requests = Request.query.filter_by(seeker_id=user_id).order_by(Request.created_at.desc()).all()
        return jsonify([req.to_dict() for req in requests]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@request_bp.route('/<int:request_id>/approve', methods=['PATCH'])
@jwt_required()
def approve_request(request_id):
    """
    Approve a request (only the giver can approve)
    This reveals the giver's phone number to the seeker
    """
    try:
        user_id = get_jwt_identity()
        request = Request.query.get(request_id)
        
        # Check if request exists
        if not request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if user is the giver of this item
        if request.item.giver_id != int(user_id):
            return jsonify({'error': 'You can only approve requests for your own items'}), 403
        
        # Check if request is still pending
        if request.status != 'pending':
            return jsonify({'error': f'This request is already {request.status}'}), 400
        
        # Check if item is still available
        if not request.item.is_available:
            return jsonify({'error': 'This item is no longer available'}), 400
        
        # Approve this request
        request.status = 'approved'
        request.updated_at = datetime.utcnow()
        
        # Reject all other pending requests for this item
        other_requests = Request.query.filter(
            Request.item_id == request.item_id,
            Request.id != request_id,
            Request.status == 'pending'
        ).all()
        
        for req in other_requests:
            req.status = 'rejected'
            req.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Request approved successfully. Phone number revealed.',
            'request': request.to_dict()  # This will include giver_phone now
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@request_bp.route('/<int:request_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_request(request_id):
    """
    Reject a request (only the giver can reject)
    """
    try:
        user_id = get_jwt_identity()
        request = Request.query.get(request_id)
        
        # Check if request exists
        if not request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if user is the giver of this item
        if request.item.giver_id != int(user_id):
            return jsonify({'error': 'You can only reject requests for your own items'}), 403
        
        # Check if request is still pending
        if request.status != 'pending':
            return jsonify({'error': f'This request is already {request.status}'}), 400
        
        # Reject the request
        request.status = 'rejected'
        request.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Request rejected',
            'request': request.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@request_bp.route('/<int:request_id>/complete', methods=['PATCH'])
@jwt_required()
def complete_request(request_id):
    """
    Mark a request as completed (after pickup)
    Only the giver can mark as complete
    """
    try:
        user_id = get_jwt_identity()
        request = Request.query.get(request_id)
        
        # Check if request exists
        if not request:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if user is the giver
        if request.item.giver_id != int(user_id):
            return jsonify({'error': 'Only the giver can mark requests as complete'}), 403
        
        # Check if request is approved
        if request.status != 'approved':
            return jsonify({'error': 'Only approved requests can be marked as complete'}), 400
        
        # Mark as completed
        request.status = 'completed'
        request.updated_at = datetime.utcnow()
        
        # Mark item as given (not available)
        request.item.is_available = False
        
        db.session.commit()
        
        return jsonify({
            'message': 'Request marked as completed',
            'request': request.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500