import React, { useState, useEffect} from 'react';
import logo from '../assets/logo.svg'
import {Link} from 'react-router-dom'

const Navigate = () => {
	const [isAuth,setIsAuth] = useState(false)
	useEffect(() => {
		if(localStorage.getItem('access_token') !== null){
			setIsAuth(true);
		}
	},[isAuth]);
  return (

  <>

      <div class="navbar">
      <Link to="/pic" className='nav-item'>Pic</Link>
      <img src={logo} alt="logo" className="logo nav-item" />
        {isAuth ? <Link to="/logout" className='nav-item'>Logout</Link> : <Link to="/login" className='nav-item'>Login</Link>}          
      </div>
  </>       
  )
}

export default Navigate