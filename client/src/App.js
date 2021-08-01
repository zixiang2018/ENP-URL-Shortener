import React, {Component} from 'react'
import { BrowserRouter as Router, Route, Link} from "react-router-dom";
import UrlShortener from "./components/urlShortener.components";
import About from "./components/about.components";

class App extends Component {
  render(){
    return(
      <Router className="container-fluid">
          <div >
           <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                  <div className="navbar-nav">
                    <Link to="/" className="navbar-brand font-link">TinyLinker</Link>
                    <Link to="/" className="navbar-brand font-weight-bold nav-font">Home</Link>
                    <Link to="/about" className="navbar-brand font-weight-bold nav-font">About</Link>
                  </div>
              </div>
              </nav>
            </div>
            <div className="container mt-5" >
              <Route path="/" exact component={UrlShortener} />\
              <Route path="/about" exact component={About} />
            </div>
      </Router>
    )
  }
}

export default App;
