import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';

import App from './App';
import Start from './pages/start';
import AboutUs from './pages/AboutUs';
import LoginPage from './pages/LoginPage';
import ErrorPage from './pages/ErrorPage';
import Billing from './pages/Pricing';
import AccountPage from './pages/AccountPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
      },
      {
        path: 'start',
        element: <Start />,
      },
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'about',
        element: <AboutUs />,
      },
      {
        path: 'billing',
        element: <Billing/>,
      },
      {
        path: 'account',
        element: <AccountPage />,
      },
    ],
  },
]);

const rootElement = document.getElementById('root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(<RouterProvider router={router} />);
}