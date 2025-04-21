// // import logo from './logo.svg';
// // import './App.css';

// // function App() {
// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         <img src={logo} className="App-logo" alt="logo" />
// //         <p>
// //           Edit <code>src/App.js</code> and save to reload.
// //         </p>
// //         <a
// //           className="App-link"
// //           href="https://reactjs.org"
// //           target="_blank"
// //           rel="noopener noreferrer"
// //         >
// //           Learn React
// //         </a>
// //       </header>
// //     </div>
// //   );
// // }

// // export default App;
// import ReactDOM from "react-dom/client";
// import { BrowserRouter, Routes, Route } from "react-router-dom";
// import Container from "react-bootstrap/Container";
// import Nav from "react-bootstrap/Nav";
// import Navbar from "./Navbar/Navbar";
// import NavDropdown from "react-bootstrap/NavDropdown";
// import Books from "./Pages/books";
// import Laptop from "./Pages/laptops";
// import Mobile from "./Pages/mobile";
// // import Telivisions from "./Pages/televisions";
// // import Layout from "./pages/Layout";
// // import Home from "./pages/Home";
// // import Blogs from "./pages/Blogs";
// // import Contact from "./pages/Contact";
// // import NoPage from "./pages/NoPage";

// function Telivisions() {
//   return (
//     <div>
//       <h3>Telivisions surendra</h3>
//     </div>
//   );
// }
// export default function App() {
//   return (
//     <BrowserRouter>
//       <Navbar />
//       <Routes>
//         <Route path="/" element={<Books />}>

//           {/* <Route path="*" element={<NoPage />} /> */}
//         </Route>
//       </Routes>
//     </BrowserRouter>
//   );
// }
// App.js
import React from "react";
// import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Link } from "react-router-dom";
import "./App.css";
// import NavBar from "./Pages/NavBar";
import Home from "./Pages/Home";
import About from "./Pages/About";
import Contact from "./Pages/Contact";
import CompanyInfo from "./Pages/Company";

// const App = () => {
//   return (
//     <BrowserRouter>
//       <NavBar />
//       <Routes>
//         <Route path="/" exact component={Home} />
//         <Route path="/about" component={About} />
//         <Route path="/contact" component={Contact} />
//       </Routes>
//     </BrowserRouter>
//   );
// };

const NavBar = () => {
  return (
    // <nav>
    //   <div class="mid">
    //     <ul>
    //       <li>
    //         <Link to="/">Home</Link>
    //       </li>
    //       <li>
    //         <Link to="/about">About</Link>
    //       </li>
    //       <li>
    //         <Link to="/contact">Contact</Link>
    //       </li>
    //     </ul>
    //   </div>
    // </nav>
    <header class="header">
      <div class="mid">
        <ul class="navbar">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/laptop">Laptop</Link>
          </li>
          <li>
            <Link to="/contact">Contact</Link>
          </li>
          <li>
            <Link to="/company">Company Info</Link>
          </li>
        </ul>
      </div>
    </header>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/laptop" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/company" element={<CompanyInfo />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
