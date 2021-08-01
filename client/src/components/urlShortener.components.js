import React,{useState} from 'react';
import {Button,Form} from 'react-bootstrap';
import axios from 'axios'


const URLShortener = ()=>{
    const [originalURL, setOriginalURL] = useState("")
    const [shortURL, setShortURL] = useState({
        url:"",
        message:""
    })

    const baseURL = window.location.origin
    
    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
      }

    const errorMessage = () =>{
        return shortURL.message && <span className="alert alert-danger">{capitalize(shortURL.message)}</span>
    }

    const successMessage = () => {
        return shortURL.url && <span className="alert alert-success">Your shortened URL: <a href={shortURL.url} target="_blank">{shortURL.url}</a></span>
    }
    const makeShortURL = async ()=>{    
        return axios.post("http://localhost:5000/api/shorten_url",{
            original_url: originalURL,
          })
            .then(res => {
                console.log(res)
                if (res.data.success){
                    setShortURL({...shortURL, url: "http://localhost:5000/api/"+res.data.shortened_url, message:""})
                }else{
                    setShortURL({...shortURL, message:res.data.message})
                }
                
            })
            .catch((error)=>{
                setShortURL({...shortURL, message:error.response.data.message})
            })
    }
    return (
        <div className="card p-5 text-white bg-info mb-3" style= {{width: "25rem"}}>
            <form className="form">
                <div className="form-group mb-2">
                    <label for="inputURL" className="mr-3">Enter a long URL to make a shorter URL</label>
                    <input type="text" value={originalURL}  onChange={e => setOriginalURL( e.target.value)} className="form-control mr-3" id="inputURL" placeholder="E.g. https://www.google.com"/>
                </div>
                <button type="button" className="btn btn-primary mb-2" onClick={()=>makeShortURL()}>Shorten URL!</button>
            </form>
            {successMessage()}
            {errorMessage()}
        </div>
    )
    
}

export default URLShortener
