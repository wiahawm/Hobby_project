<template>
  <div id="naver_id_login"></div>
</template>

<script>
export default {
  name: 'NaverLogin',
  data () {
    return {
      naver_id_login: ''
    }
  },
  mounted () {
    this.naver_id_login = new naver_id_login(
      'IaquHgHTmPlf_gc_a8es',
      'http://localhost:8080/login'
    )
    let state = this.naver_id_login.getUniqState()
    this.naver_id_login.setButton('green', 4, 48)
    this.naver_id_login.setDomain('http://127.0.0.1:8000/')
    this.naver_id_login.setState(state)
    this.naver_id_login.setPopup()
    this.naver_id_login.init_naver_id_login()
  },
  methods: {
  }
}
</script>
