/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'cheermoon', // the auth0 domain prefix
    audience: 'COFFEE_SHOP', // the audience set for the auth0 app
    clientId: 'L3p1j1Q7VH5RHbJZiI39532zLPC7ZZnv', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
