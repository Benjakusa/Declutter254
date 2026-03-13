import StatusBadge from "./StatusBadge"

function RequestList({ requests }) {

  if (!requests || requests.length === 0) {
    return <p>No requests yet</p>
  }

  return (

    <div>

      {requests.map((req) => (

        <div key={req.id} style={{border:"1px solid #ccc", padding:"10px", margin:"10px"}}>

          <p><strong>Item:</strong> {req.item_title}</p>

          <p><strong>Message:</strong> {req.message}</p>

          <StatusBadge status={req.status} />

        </div>

      ))}

    </div>

  )

}

export default RequestList 