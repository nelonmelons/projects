import React from 'react';
import { Helmet } from 'react-helmet';
import Header from '../components/header';

const Portfolio = () => (
  <>
    <Helmet>
      <title>My Portfolio</title>
      <meta name="description" content="My portfolio page showcasing my projects." />
    </Helmet>
    <Header />
    <main>
      {/* Content */}
    </main>
  </>
);
