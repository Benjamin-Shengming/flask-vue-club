<template>
  <div> 
    <b-navbar toggleable="md" type="dark" variant="info">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand href="#">{{ clubName }}</b-navbar-brand>
    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item :href="urlHome">首页</b-nav-item>
        <b-nav-item :href="urlAdmin">管理</b-nav-item>
      </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>
        <b-nav-item-dropdown right>
          <!-- Using button-content slot -->
          <template slot="button-content">
            <em>User</em>
          </template>
            <div v-if="isLoggedIn">
          <b-dropdown-item href="#" @click="logout()"<</b-dropdown-item>
            </div>
            <div v-else>
          <b-dropdown-item :href="urlLogin">Signin</b-dropdown-item>
          </div>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
    </b-navbar>

    <div v-if="serviceBook">
      <ServiceBook :service="singleService"></ServiceBook>
    </div>
    <div v-else>
    <b-carousel id="carousel1"
                style="text-shadow: 1px 1px 2px #333;"
                controls
                indicators
                background="#ababab"
                :interval="4000"
                img-width="1024"
                img-height="360"
                v-model="slide"
                @sliding-start="onSlideStart"
                @sliding-end="onSlideEnd" >
      <!-- Slide with blank fluid image to maintain slide aspect ratio -->
      <b-carousel-slide 
          v-for="item in headlineServiceArray"
          v-bind:key="item.id"
          :caption="item.name"  
          :text="item.description">
          <img slot="img" class="d-block img-fluid w-100" width="1024" height="480"
             :src="getServiceMajorPic(item)" 
             :alt="item.description"
             @click="bookService(item)">
      </b-carousel-slide>
    </b-carousel>
    <p class="mt-4 invisible">
      Slide #: {{ slide }}<br>
      Sliding: {{ sliding }}
    </p>
    <div class="card">
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="item in serviceArray" v-bind:key="item.id">
          <b-card @click="bookService(item)"> 
            <b-media > 
              <b-img :src="getServiceMajorPic(item)" 
                  slot="aside" 
                  blank-color="#ccc" 
                  width="200" height='200' :alt="item.name" />
              <h5 class="mt-0">{{ item.name }}</h5>
              <p>
                {{ item.description }}
             </p>
             <b-button href="#" variant="primary">我要去...</b-button>
            </b-media> 
          </b-card>
        </li>
      </ul>
    </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ServiceBook from "./ServiceBook.vue";
import UserLogin from "./UserLogin.vue";
// import jQuery from "jquery";
import { getBackendAPIURI,
         prefixAPIURIPath,
         prefixClubName,
         prefixFileStore,
         prefixService
         //getServiceFileStorePath
        } from "./genlib.js";

export default {
  components: {
    ServiceBook,
    UserLogin
  },
  data () {
    return {
      serviceBook: false,
      singleService: null,
      serviceArray: [],
      headlineServiceArray: [],
      slide: 0,
      sliding: null
    };
  },
  computed: {
    clubName: function () {
      return this.$route.params.club_name
    },
    urlAdmin: function () {
      return '/' + this.clubName + '/admin'
    },
    urlHome: function() {
      return "/" + this.clubName;
    },
    urlLogin: function() {
      return "/" + this.clubName + '/user/login'
    },
    urlLogout: function() {
      return "/" + this.clubName + '/user/logout'
    },
    isLoggedIn: function() {
      localStorage.getItem('usertoken')
    }

  },
  methods: {
    onSlideStart (slide) {
      this.sliding = true
    },
    onSlideEnd (slide) {
      this.sliding = false
    },
    viewMoreService() {
      console.log("viewMoreService");
    },
    bookService(item) {
      console.log(item);
      console.log("show service " + item.id);
      this.singleService = item;
      this.serviceBook = true;
    },
    logout() {
      localStorage.removeItem('usertoken')
    },
    getServiceMajorPic(item) {
      let url = prefixAPIURIPath(prefixFileStore(
                                prefixClubName(this.clubName,
                                    prefixService("/" + item.id + "/" + item.major_pic)
                            )))
      url = getBackendAPIURI(window.location.href, url);
      console.log(url)
      return url;
    },
    getService() {
      let servicePath = prefixAPIURIPath(
                            prefixClubName(this.clubName,
                            prefixService("")));
      let url = getBackendAPIURI(window.location.href, servicePath);
      console.log(url)
      axios.get(url).then((response) => {
        console.log(response)
        this.serviceArray = response.data
        for (let item of this.serviceArray) {
          if (item.slide) {
            console.log(item)
            this.headlineServiceArray.push(item)
          }
        }
        console.log(this.serviceArray)
        console.log(this.headlineServiceArray)
      }).catch((error) => {
        console.log(error)
        console.log('redirect to not found page')
        this.$router.push('no_found/404');
      });
    }
  },
  mounted () {
    console.log("mounted");
  },
  created () {
    console.log("created");
    this.getService()
  }
};
</script>
