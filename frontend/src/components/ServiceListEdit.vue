<template>
  <div fluid> 
    <b-container fluid>
      <b-row fluid>
      <b-col v-for="item in serviceArray" v-bind:key="item.id" >
      <b-card  
              :img-src="getServiceMajorPic(item)"
              :img-alt="item.name"
              style="max-width: 20rem;"
              class="mb-2"
              
              @click="gotoService(item)"> 
          <p class="card-text">
            {{ item.description }}
          </p>
          <b-button href="#" variant="primary">Delete</b-button>
          <b-button href="#" variant="primary">Edit...</b-button>
      </b-card>
      </b-col>
      </b-row>
    </b-container>

  </div>
</template>

<script>
import axios from "axios";
// import jQuery from "jquery";
import {
  getBackendAPIURI,
  prefixAPIURIPath,
  prefixClubName,
  prefixFileStore,
  prefixService
  //getServiceFileStorePath
} from "./genlib.js";

export default {
  data() {
    return {
      serviceArray: []
    };
  },
  computed: {
    clubName: function() {
      return this.$route.params.club_name;
    },
    urlAdmin: function() {
      return "/" + this.clubName + "/admin";
    }
  },
  methods: {
    viewMoreService() {
      console.log("viewMoreService");
    },
    gotoService(item) {
      console.log(item);
      console.log("show service " + item.id);
    },
    getServiceMajorPic(item) {
      let url = prefixAPIURIPath(
        prefixFileStore(
          prefixClubName(
            this.clubName,
            prefixService("/" + item.id + "/" + item.major_pic)
          )
        )
      );
      url = getBackendAPIURI(window.location.href, url);
      console.log(url);
      return url;
    },
    getService() {
      let servicePath = prefixAPIURIPath(
        prefixClubName(this.clubName, prefixService(""))
      );
      let url = getBackendAPIURI(window.location.href, servicePath);
      console.log(url);
      axios.get(url).then(response => {
        this.serviceArray = response.data;
        for (let item of this.serviceArray) {
          if (item.slide) {
            console.log(item);
            this.headlineServiceArray.push(item);
          }
        }
        console.log(this.serviceArray);
        console.log(this.headlineServiceArray);
      });
    }
  },
  mounted() {
    console.log("mounted");
  },
  created() {
    console.log("created");
    this.getService();
  }
};
</script>
