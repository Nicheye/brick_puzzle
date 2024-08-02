import React,{useState} from 'react'
import axios from 'axios'
// Define the Login function.
const Login = () => {
  const [email,setEmail] = useState('');
// Create the submit method.
  const submit = async e =>{
    e.preventDefault()

    const user = {
      email:email
    };
// Create the POST requuest
const config = {
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
};

const { data } = await axios.post('http://localhost:8000/auth/login/', user, config);
  localStorage.clear();
  console.log(data.access)
  localStorage.setItem('access_token',data.access);
  localStorage.setItem('refresh_token',data.refresh);
  axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
  window.location.href = '/'
  }

  return (
    <>
    <form className="Auth-form" onSubmit={submit}>
      <div className="Auth-form-content">
        <h3 className="Auth-form-title">Sign In</h3>
        
        <div className="form-group mt-3">
          <label>email</label>
          <input name='email' 
            type="email"     
            className="form-control mt-1"
            placeholder="Enter email"
            value={email}
            required
            onChange={e => setEmail(e.target.value)}/>
        </div>
        <div className="d-grid gap-2 mt-3">
          <button type="submit" 
             className="btn btn-primary">Submit</button>
        </div>
      </div>
   </form>
   </>
  )
}

export default Login