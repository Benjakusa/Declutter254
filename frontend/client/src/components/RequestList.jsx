import StatusBadge from "./StatusBadge"
import RequestActions from "./RequestActions"

function RequestList({ requests, refreshRequests }) {

  if (!requests || requests.length === 0) {
    return <p>No requests yet</p>
  }

  return (

    <div>

      {requests.map((req) => (

        <div
          key={req.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            margin: "10px",
            borderRadius: "6px"
          }}
        >

          <p>
            <strong>Item:</strong> {req.item_title}
          </p>

          <p>
            <strong>Message:</strong> {req.message}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            <StatusBadge status={req.status} />
          </p>

          <RequestActions
            request={req}
            refreshRequests={refreshRequests}
          />

        </div>

      ))}

    </div>

  )

}

export default RequestList 