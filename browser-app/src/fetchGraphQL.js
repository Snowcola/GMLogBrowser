// your-app-name/src/fetchGraphQL.js
async function fetchGraphQL(text, variables) {
    const REACT_APP_GITHUB_AUTH_TOKEN = process.env.REACT_APP_GITHUB_AUTH_TOKEN;
  
    // Fetch data from GitHub's GraphQL API:
    const response = await fetch('http://127.0.0.1:5000/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: text,
        variables,
      }),
    });
  
    // Get the response as JSON
    return await response.json();
  }
  
  export default fetchGraphQL;