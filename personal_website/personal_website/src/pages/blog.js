import React from 'react';
import { graphql, Link } from 'gatsby';
import Header from '../components/header';

const BlogPage = ({ data }) => (
  <>
    <Header />
    <main>
      <h1>Blog</h1>
      {data.allMarkdownRemark.edges.map(({ node }) => (
        <article key={node.id}>
          <h2>
            <Link to={node.fields.slug}>{node.frontmatter.title}</Link>
          </h2>
          <p>{node.excerpt}</p>
        </article>
      ))}
    </main>
  </>
);

export const query = graphql`
  {
    allMarkdownRemark(sort: { frontmatter: { date: DESC } }) {
      edges {
        node {
          id
          frontmatter {
            title
          }
          fields {
            slug
          }
          excerpt
        }
      }
    }
  }
`;

export default BlogPage;
