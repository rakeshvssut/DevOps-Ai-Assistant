// About.js
import React from "react";
import mobilesData from "./mobiles.json";

const About = () => {
  return (
    <div>
      <h3 className="justify-content-center">Laptop List</h3>
      <ul className="grid gap-4 ul-list">
        {mobilesData.map((mobile) => (
          <li
            key={mobile.id}
            className="flex items-center gap-4 p-4 bg-gray-100 rounded"
          >
            <img
              src="https://media.istockphoto.com/id/1408387705/photo/social-media-marketing-social-issues-social-gathering.jpg?s=612x612&w=0&k=20&c=JV30g8nar60CKJnpruS6S4GS7WXQHG9BUi-j4a056PQ="
              alt={`${mobile.brand} ${mobile.model}`}
              className="w-16 h-16"
            />
            <div>
              <strong>{mobile.brand}</strong> - {mobile.model} (${mobile.price})
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default About;
