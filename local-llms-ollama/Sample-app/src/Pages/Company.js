import React, { useEffect, useState } from "react";

const CompanyInfo = () => {
  const [awsRegion, setAwsRegion] = useState("Unknown AWS Region");

  useEffect(() => {
    const fetchAwsRegion = async () => {
      try {
        const res = await fetch('http://169.254.169.254/latest/dynamic/instance-identity/document');
        const data = await res.json();
        const region = data.region;
        setAwsRegion(region);
      } catch (error) {
        console.error("Error fetching AWS region:", error);
      }
    };

    fetchAwsRegion();
  }, []);

  return (
    <div className="container">
      <div className="company-info">
        <p>
          Welcome to NEXTURN Company! We are a leading provider of innovative
          solutions in AWS region: {awsRegion}. With our dedication to
          excellence and customer satisfaction, we aim to deliver the best
          services to our clients. Our team of experts is committed to pushing
          boundaries and achieving remarkable results.
        </p>
      </div>
    </div>
  );
};

export default CompanyInfo;
