<template>
  <div fluid> 
    <b-container fluid>
    <div class="card">
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="item in serviceArray" v-bind:key="item.id">
          <b-card @click="gotoService(item)"> 
            <b-media > 
              <b-img :src="getServiceMajorPic(item)" 
                  slot="aside" 
                  blank-color="#ccc" 
                  width="200" height='200' :alt="item.name" />
              <h5 class="mt-0">{{ item.name }}</h5>
              <p>
                {{ item.description }}
             </p>
            </b-media> 
             <b-button href="#" variant="primary" fluid-grow>删除此服务产品</b-button>
             <b-button href="#" variant="primary" fluid-grow>修改服务产品...</b-button>
          </b-card>
        </li>
      </ul>
    </div>
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
