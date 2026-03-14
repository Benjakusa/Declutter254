// Fetch all items
export function fetchItems(){

  return fetch("/items")
    .then(res => res.json())

}


// Fetch single item
export function fetchItem(id){

  return fetch(`/items/${id}`)
    .then(res => res.json())

}


// Create item
export function createItem(formData){

  return fetch("/items",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body: JSON.stringify(formData)
  })
  .then(res => res.json())

}


// Update item
export function updateItem(id, formData){

  return fetch(`/items/${id}`,{
    method:"PATCH",
    headers:{
      "Content-Type":"application/json"
    },
    body: JSON.stringify(formData)
  })
  .then(res => res.json())

}


// Delete item
export function deleteItem(id){

  return fetch(`/items/${id}`,{
    method:"DELETE"
  })

}


// Mark item as given
export function markAsGiven(id){

  return fetch(`/items/${id}/given`,{
    method:"PATCH"
  })
  .then(res => res.json())

}


// Create request
export function createRequest(itemId, message){

  return fetch("/requests",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body: JSON.stringify({
      item_id: itemId,
      message: message
    })
  })
  .then(res => res.json())

}


// Fetch incoming requests (for item owner)
export function fetchIncomingRequests(){

  return fetch("/requests/incoming")
    .then(res => res.json())

}


// Fetch outgoing requests (for requester)
export function fetchOutgoingRequests(){

  return fetch("/requests/outgoing")
    .then(res => res.json())

}


// Approve request
export function approveRequest(requestId){

  return fetch(`/requests/${requestId}/approve`,{
    method:"PATCH"
  })
  .then(res => res.json())

}


// Reject request
export function rejectRequest(requestId){

  return fetch(`/requests/${requestId}/reject`,{
    method:"PATCH"
  })
  .then(res => res.json())

} 