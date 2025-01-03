import React from 'react';
import { Helmet } from 'react-helmet';
import '../assets/Pricing.css';

const Pricing = () => {
  return (
    <div className="pricing">
      <Helmet>
        <title>Pix2Print - Billing</title>
      </Helmet>
      <h1>Pricing</h1>
      <div className="pricing-table">
        <div className="item">
          <h2>Basic</h2>
          <p>For small projects, lower resolution</p>
          <p>Free</p>
          <button>Select</button>
        </div>
        <div className="item">
          <h2>Enthusiast</h2>
          <p>For higher resolution projects</p>
          <p>$10/month</p>
          <button>Select</button>
        </div>
        <div className="item">
          <h2>Business</h2>
          <p>For manufacturing use</p>
          <p>$15/month</p>
          <button>Select</button>
        </div>
        <div className="item instructor">
          <h2>Instructor/TA</h2>
          <p>If you're a coding Bootcamp instructor/TA (ie Justin)</p>
          <p>$150/month</p>
          <div className="instructor-img">
            <img src="../assets/images/oiledUP.jpg" alt="Instructor" />
          </div>
          <button>Select</button>
        </div>
      </div>
    </div>
  );
};

export default Pricing;
