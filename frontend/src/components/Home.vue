<template>
  <div> 
    <b-navbar toggleable="md" type="dark" variant="info">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand href="#">{{ clubName }}</b-navbar-brand>
    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item :href="urlAdmin">管理</b-nav-item>
      </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>
        <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">ES</b-dropdown-item>
          <b-dropdown-item href="#">RU</b-dropdown-item>
          <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown right>
          <!-- Using button-content slot -->
          <template slot="button-content">
            <em>User</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Signout</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
    </b-navbar>

    <b-carousel id="carousel1"
                style="text-shadow: 1px 1px 2px #333;"
                controls
                indicators
                background="#ababab"
                :interval="4000"
                img-width="1024"
                img-height="480"
                v-model="slide"
                @sliding-start="onSlideStart"
                @sliding-end="onSlideEnd" >
      <!-- Text slides with image -->
      <b-carousel-slide caption="First slide"
                        text="Nulla vitae elit libero, a pharetra augue mollis interdum."
                        img-src="https://lorempixel.com/1024/480/technics/2/" />

      <!-- Slides with custom text -->
      <b-carousel-slide img-src="https://lorempixel.com/1024/480/technics/4/">
        <h1>Hello world!</h1>
      </b-carousel-slide>

      <!-- Slides with image only -->
      <b-carousel-slide img-src="https://lorempixel.com/1024/480/technics/8/">
      </b-carousel-slide>

      <!-- Slides with img slot -->
      <!-- Note the classes .d-block and .img-fluid to prevent browser default image alignment -->
      <b-carousel-slide>
        <img slot="img" class="d-block img-fluid w-100" width="1024" height="480"
             src="https://lorempixel.com/1024/480/technics/5/" alt="image slot">
      </b-carousel-slide>

      <!-- Slide with blank fluid image to maintain slide aspect ratio -->
      <b-carousel-slide caption="Blank Image" img-blank img-alt="Blank image">
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
          eros felis, tincidunt a tincidunt eget, convallis vel est. Ut pellentesque
          ut lacus vel interdum.
        </p>
      </b-carousel-slide>
    </b-carousel>

    <p class="mt-4">
      Slide #: {{ slide }}<br>
      Sliding: {{ sliding }}
    </p>

    <div class="card">
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <b-card> <b-media>
            <b-img src="https://lorempixel.com/1024/480/technics/5/" 
                  slot="aside" 
                  blank-color="#ccc" 
                  width="256" height='256' alt="placeholder" />
            <h5 class="mt-0">远岛七日游</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
              sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
              Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis
              in faucibus.
            </p>
            <b-button href="#" variant="primary">我要去...</b-button>
          </b-media> </b-card>

        </li>

        <li class="list-group-item">
          <b-card> <b-media right-align vertical-align="center">
            <b-img src="https://lorempixel.com/1024/480/technics/5/" 
                  slot="aside" 
                  blank-color="#ccc" 
                  width="256" height='256' alt="placeholder" />
            <h5 class="mt-0">远岛七日游</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
              sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
              Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis
              in faucibus.
            </p>
            <b-button href="#" variant="primary">我要去...</b-button>
          </b-media> </b-card>
        </li>

        <li class="list-group-item">
          <b-card> <b-media >
            <b-img src="https://lorempixel.com/1024/480/technics/5/" 
                  slot="aside" 
                  blank-color="#ccc" 
                  width="256" height='256' alt="placeholder" />
            <h5 class="mt-0">远岛七日游</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
              sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
              Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis
              in faucibus.
            </p>
            <b-button href="#" variant="primary">我要去...</b-button>
          </b-media> </b-card>
        </li>

        <li> 
          <b-button variant="primary" @click="viewMoreService()">查看更多...</b-button>
        </li>
      </ul>
    </div>
    <p> {{ endIndex }} </p>
  </div>
</template>

<script>
import axios from "axios";
// import jQuery from "jquery";
import { getBackendAPIURI,
         prefixAPIURIPath,
         prefixClubName,
         // prefixFileStore,
         prefixService
         //getServiceFileStorePath
        } from "./genlib.js";

export default {
  data () {
    return {
      endIndex: 0,
      serviceArray: [],
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
    getService() {
      let servicePath = prefixAPIURIPath(
                            prefixClubName(this.clubName,
                            prefixService("")));
      let url = getBackendAPIURI(window.location.href, servicePath);
      console.log(url)
      axios.get(url).then((reponse) => {
        console.log(reponse)
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