/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { Link } from 'react-router-dom';
import Login from './Login';
function Navbar() {
    return (
        <div className="navbar bg-base-100">
            <div className="navbar-start">
                <details className="dropdown">
                    <summary className="btn btn-ghost btn-circle" tabIndex={0} role="button">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" /></svg>
                    </summary >
                        <ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                            <li><a><Link to="/">Home</Link></a></li>
                            <li><a><Link to="/calendar">Calendar</Link></a></li>
                        </ul>
                </details>
            </div>
            <div className="navbar-center">
                <a className="btn btn-ghost text-xl"><Link to="/">Better Calendar</Link></a>
            </div>
            <div className="navbar-end">
            <Login />
            </div>
        </div>
    );
}

export default Navbar;