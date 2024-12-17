import { useState, useEffect } from 'react';
import { fetchData } from '../api/API';
import Template from '../interfaces/interfaces';

const TemplateSearch = () => {
  const [item, setItem] = useState<Template | null>(null);
  const [savedItems, setSavedItems] = useState<Template[]>([]);

  useEffect(() => {
    fetchItem();
  }, []);

  const fetchItem = async () => {
    const items = await fetchData('https://api.example.com/items');
    if (items.length > 0) {
      setItem(items[0]);
    } else {
      setItem(null);
    }
  };

  const saveItem = () => {
    if (item) {
      const updatedSavedItems = [...savedItems, item];
      setSavedItems(updatedSavedItems);
      localStorage.setItem('savedItems', JSON.stringify(updatedSavedItems));
      fetchItem();
    }
  };

  const skipItem = () => {
    fetchItem();
  };

  return (
    <div>
      {item ? (
        <div>
          <h2>{item.name}</h2>
          <p>Location: {item.location}</p>
          <p>Email: {item.email}</p>
          <p>Company: {item.company}</p>
          <button onClick={saveItem}>+</button>
          <button onClick={skipItem}>-</button>
        </div>
      ) : (
        <p>No more items available</p>
      )}
    </div>
  );
};

export default TemplateSearch;