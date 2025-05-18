import React, { useState, useEffect} from "react";
import { useParams } from "react-router-dom";

const ItemDetail = () => {
    const { id } = useParams();
    const [item, setItem] = useState(null);
    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/items/${id}/`)
        .then((res) => res.json())
        .then((data) => setItem(data))
        .catch((err) => console.error("エラー:", err));
    }, [id]);
    if (!item) {return <p>読み込み中...</p>;
    }
    return (
        <div>
            <h2>{item.name}</h2>
            <p>価格: ¥{item.price}</p>
            <p>{item.information}</p>
            <img src={item.image} alt={item.name} style={{ width: '300px'}} />
        </div>
    );
};

export default ItemDetail;
