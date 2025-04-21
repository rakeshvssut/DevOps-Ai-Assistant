import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { init as initApm } from "@elastic/apm-rum";
import "bootstrap/dist/css/bootstrap.min.css";

initApm({
  // serviceName: "my-service-name",
  // serverUrl:
  //   "https://4f484e39eae04b01bd5ea6a5494746fb.apm.us-central1.gcp.cloud.es.io:443",
  // //https://4f484e39eae04b01bd5ea6a5494746fb.apm.us-central1.gcp.cloud.es.io:44
  // // Set the service version (required for source map feature)
  // serviceVersion: "",
  // environment: process.env.NODE_ENV || "development",
  serviceName: "test-react-app",

  secretToken: "KfbNsWrYUtId9GdQtc",

  serverUrl:
    "https://aa14675c565c4437b58187566bcfc11c.apm.ap-south-1.aws.elastic-cloud.com:443",

  environment: "my-environment",
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
