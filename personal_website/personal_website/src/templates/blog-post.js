import React from 'react';
import { graphql } from 'gatsby';

const BlogPost = ({ data }) => {
  const post = data.markdownRemark;
  return (
    <>
      <Header />
      <main>
        <h1>{post.frontmatter.title}</h1>
        <div dangerouslySetInnerHTML={{ __html: post.html }} />
      </main>
    </>
  );
};

export const query = graphql`
  query($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      frontmatter {
        title
      }
    }
  }
`;

export default BlogPost;
