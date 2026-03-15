import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchItem } from "../api/api";
import RequestForm from "../components/RequestForm";

function ItemDetail() {

  const { id } = useParams();

  const [item, setItem] = useState(null);

  useEffect(()=>{

    fetchItem(id).then(data => {
      setItem(data);
    });

  },[id]);

  if(!item) return <h2>Loading...</h2>;

  return (

    <div>

      <h2>{item.title}</h2>

      <p>{item.description}</p>

      <p>Category: {item.category}</p>

      <p>Condition: {item.condition}</p>

      <p>Location: {item.location}</p>

      <p>Pickup Days: {item.pickup_days}</p>

      <p>Pickup Times: {item.pickup_times}</p>

      <RequestForm itemId={item.id}/>

    </div>

  );
}

export default ItemDetail; 