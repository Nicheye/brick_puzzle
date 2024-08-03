import React from 'react'
import { useEffect,useState } from 'react'
import axios from 'axios'
import ImageList from './ImageList'
import PromptForm from './PromptForm'
const Home = () => {
  const [message,setMessage] = useState('');
  const [images,setImage] = useState([]);

  useEffect(() => {
    if(localStorage.getItem('access_token') ===null){
      window.location.href = '/login'

    }
    else{
      (async () =>{
        try{
          const {data} = await axios.get(
            'http://localhost:8000/api/v1/',{
              headers:{
                'Content-Type':'application/json'
              },
              withCredentials:true,
            }
          );
          setMessage(data.message);
          setImage(data.images)
        }
        catch (e){
          console.log('not auth')
        }
      })()};
  },[]);
  if (message == 'generate your image'){
    return (
      <>
      <h1 class="mt-10 mb-8 text-4xl font-extrabold leading-none tracking-tight text-white md:text-5xl lg:text-6xl dark:text-white text-center">
        Generate 
        <span class=" ml-5 mr-5 p-1 pl-2 pr-2 pb-3 bg-blue-400 text-black px-1">your image</span>
        and see other images
      </h1>


      <PromptForm/>
      <ImageList images={images}/>
      </>
    )
  }
  return (
    <>
    
    <ImageList images={images}/>
    </>
  )
}

export default Home