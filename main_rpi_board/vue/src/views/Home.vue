<template>
  <div class="home">
      <p>Loftslamper</p>
      <button type = "button" v-on:click="ikea_lights('On')">Tænd</button>
      <button type = "button" v-on:click="ikea_lights('Off')">Sluk</button><br>
      <p>Dæmpning</p>
      <button type = "button" v-on:click="ikea_lights(25)">25</button>
      <button type = "button" v-on:click="ikea_lights(50)">50</button>
      <button type = "button" v-on:click="ikea_lights(75)">75</button>
      <button type = "button" v-on:click="ikea_lights(100)">100</button><br>
      <p>Skrivebords lampe</p>
      <button type = "button" v-on:click="relay('desk', 'On')">Tænd</button>
      <button type = "button" v-on:click="relay('desk', 'Off')">Sluk</button><br>
      <p>Lys kæde</p>
      <button type = "button" v-on:click="relay('chain', 'On')">Tænd</button>
      <button type = "button" v-on:click="relay('chain', 'Off')">Sluk</button><br>
  </div>
</template>

<script>

export default {
  name: 'Home',
  methods : {
    ikea_lights : function(value){
      if(typeof(value) == "string"){
        this.fetchAPICall("ikea_lights?state=" + value, "GET");
      }
      else if(typeof(value) == "number"){
        this.fetchAPICall("ikea_lights?value=" + value, "GET");
      }
    },
    relay : function (dest, state){ 
      this.fetchAPICall("relay?state=" + String(state) + "&light_source=" + String(dest), "GET")
    },
    fetchAPICall : async function (route, method) {
      let url = "http://localhost:3000/" + route
      console.log(url);
      try {
        return await fetch(url, { method: method });
      } 
      catch (err) {
        alert("Error: " + err);
      }
    },
  }
}
</script>
