import { useState, useEffect } from 'react';
import Template from '../interfaces/interfaces';

const SavedItems = () => {
  const [savedItems, setSavedItems] = useState<Template[]>([]);

  useEffect(() => {
    const items = JSON.parse(localStorage.getItem('savedItems') || '[]');
    setSavedItems(items);
  }, []);

  return (
    <div>
      {savedItems.length > 0 ? (
        savedItems.map((item, index) => (
          <div key={index}>
            <h2>{item.name}</h2>
            <p>Location: {item.location}</p>
            <p>Email: {item.email}</p>
            <p>Company: {item.company}</p> 
          </div>
        ))
      ) : (
        <p>No items have been saved</p>
      )}
    </div>
  );
};

export default SavedItems;