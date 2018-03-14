import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/no_found/no_found', component: 'NotFound' },
  { path: '/no_found/404', component: 'NotFound' },
  { path: '/:club_name', component: 'Home' },
  { path: '/:club_name/admin', component: 'Admin' },
  { path: '/:club_name/user/login', component: 'UserLogin' },
  { path: '/:club_name/user/register', component: 'UserRegister' },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
