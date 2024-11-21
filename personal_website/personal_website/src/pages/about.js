// src/pages/about.js
import React from "react"
import Header from '../components/header';
import { Helmet } from "react-helmet"

const About = () => (
  <div>
    <Helmet>
      <title>About Us - Your Site Name</title>
    </Helmet>
    <h1>About Us</h1>
    <p>This is the about page.</p>
  </div>
)

export default About