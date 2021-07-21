import React, { useState } from "react";
import "./App.css";
import NodeRSA from "node-rsa";
import axios from "axios";

function App() {
  const [pubkey1, setpubkey1] = useState({});
  const [prikey1, setprikey1] = useState({});
  const key = NodeRSA({ b: 1024 });
  let public_key = key.exportKey("public");
  let private_key = key.exportKey("private");

  //console.log(public_key);
  //console.log(private_key);

  function genarate() {
    localStorage.setItem("public", public_key);
    localStorage.setItem("private", private_key);
    window.location.reload();
  }

  function removeKey() {
    localStorage.removeItem("public");
    localStorage.removeItem("private");
    window.location.reload();
  }

  async function encrpyt() {
    // let client_key_private = new NodeRSA(localStorage.getItem("private"));
    //let client_key_public = new NodeRSA(localStorage.getItem("public"));

    const { data } = await axios.get("http://localhost:5000/getpublic1");
    setpubkey1(data.public_key_1);
    setprikey1(data.private_key_1);

    console.log(pubkey1);
    console.log(prikey1);

    let public_key_1 = new NodeRSA(pubkey1);
    let encrpy_client_key_public = public_key_1.encrypt(
      localStorage.getItem("private"),
      "base64"
    );
    console.log(encrpy_client_key_public);

    axios.post("http://localhost:5000/postClientPublicEncrypt", {
      client_encrypt_public_key: encrpy_client_key_public,
      private_key_1: prikey1,
    });

    // let encrpytString = key_public.encrypt("shaman", "base64");
    //console.log(encrpytString);

    //let decryptString = key_private.decrypt(encrpytString, "utf8");
    //console.log(decryptString);
  }

  return (
    <React.Fragment>
      <div className="App">
        <h1>Hello world </h1>
      </div>
      <div className="App">
        <p>{localStorage.getItem("public")}</p>
      </div>
      <div className="App">
        <p>{localStorage.getItem("private")}</p>
      </div>
      <div className="App">
        <button onClick={genarate}>Genarate key</button>
        <button onClick={removeKey}>Remove Key</button>
        <button onClick={encrpyt}>Encrpyt</button>
      </div>
    </React.Fragment>
  );
}

export default App;
