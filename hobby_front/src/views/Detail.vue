<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" md="5">
          <v-chip small color="#9AB878" dark>{{data.subclass}}</v-chip>
          <h1>{{data.title}}</h1>
          <h5 class="mb-2">작성 날짜: {{data.created_at}}</h5>
          <p>모집 마감: 
            <v-icon class="mr-1">mdi-calendar-month</v-icon>
              {{data.endDay}}
          </p>
        </v-col>
        <v-col cols="12" md="2">
          <v-menu
          transition="scale-transition"
          >
            <template v-slot:activator="{ on }">
              <v-chip pill v-on="on" class="mt-8">
                <v-avatar left>
                  <v-img :src="data.userimage"></v-img>
                </v-avatar>
                {{data.username}}
              </v-chip>
            </template>
            <v-card width="300">
              <v-list dark>
                <v-list-item>
                  <v-list-item-avatar>
                    <v-img :src="data.userimage"></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>{{data.username}}</v-list-item-title>
                    <v-list-item-subtitle>친절함 활발함</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon >
                      <v-icon @click="yourPage()">mdi-chevron-right</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-card>
          </v-menu>
        </v-col>
        <v-snackbar
          v-model="snackbar"
          :vertical="vertical"
          color="success"
        >
          {{ ment }}
          <div class="ml-auto">
            <v-btn
              class="ml-auto"
              color="white"
              text
              @click="snackbar = false, move()"
            >
              go
            </v-btn>
            <v-btn
              class="ml-auto"
              color="white"
              text
              @click="snackbar = false"
            >
              Close
            </v-btn>
          </div>
        </v-snackbar>
        <!-- 유저의 상태에 따라 변경되야함 -->
        <v-col cols="12" md="4" offset-md="1" class="d-flex align-center" v-if="userId !== '' & data.user !== userId">
          <!-- 모임 참여하기 함수 추가 -->
          <v-btn block dark color="#F3B749" @click="joinGroup()">참여하기</v-btn>
        </v-col>
        <v-col cols="12" md="4" offset-md="1" class="d-flex align-center" v-if="userId !== '' & data.user !== userId">
          <!-- 모임 참여 취소하기 -->
            <v-btn block dark color="red" @click="unjoinGroup()">참여 취소하기</v-btn>
        </v-col>
        <v-col  v-if="data.user === userId">
          <v-btn block dark color="#F3B749">
            <router-link 
            :to="'/list/detail/' + data.id + '/update'"
            > 
            글 수정하기
            </router-link>
          </v-btn>
          <v-btn block dark color="#F3B749" @click="deleteDetail()">글 삭제하기</v-btn>
        </v-col>
        
      </v-row>
      <v-row>
        <v-col cols="12" md="7">
          <v-img
          :src= "data.photo"
          class="mb-12"
          ></v-img>
          <v-card class="excard">
            <v-card-title class="mb-3">
              모임 소개
            </v-card-title>
            <v-card-text class="text--primary">
              <pre>{{data.contents}}</pre>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" offset-md="1">
          <v-card class="excard">
            <v-card-title class="mb-3">
              모임 정보
            </v-card-title>
            <v-card-text class="text--primary">
              
              <div class="mb-4">
                <v-icon class="mr-1">mdi-calendar-month</v-icon>
                날짜: {{data.startDay}}
              </div>
              <div class="mb-4">
                <v-icon class="mr-1">mdi-clock-outline</v-icon>
                시각: {{data.startTime}}
              </div>
              <div class="mb-4">
                <v-icon class="mr-1">mdi-map-marker</v-icon>
                장소: {{data.location}}
              </div>
              <div class="mb-4">
                <v-icon class="mr-1">mdi-account</v-icon>
                인원: 최대 {{data.member}}명 / {{data.minAge}}세 ~ {{data.maxAge}}세까지
              </div>
              <div class="mb-4">
                <v-icon class="mr-1">mdi-gender-male-female</v-icon>
                {{data.gender}}
              </div>
              <div class="mb-4">
                <v-icon class="mr-1">mdi-currency-krw</v-icon>
                예상 비용: {{data.fee}}원
              </div>
            </v-card-text>
          </v-card>
          <div class="mb-12" id="mapview">
            <!-- 지도 -->
            <MapService :address="data.location"></MapService>  
            <!-- <MapService></MapService>   -->
          </div>
          <v-card class="excard">
            <div id="member">
              <!-- 모임 멤버 관련 정보 -->
              <v-card-title class="mb-3">
                모임 멤버 ({{cnt}} / {{data.member}})
              </v-card-title>
              <div v-for="join in joins" :key="join.id"> 
                <v-chip pill class="ma-3">
                  <v-avatar left>
                    <v-img :src="join.user_image"></v-img>
                  </v-avatar>
                  {{join.user_name}}
                </v-chip>
              </div>

            </div>
          </v-card>
        </v-col>
      </v-row>
      <!-- 댓글 -->
      <CommentHobby class="mt-10"></CommentHobby>
    </v-container>
  </div>
</template>

<script>
import MapService from '../components/MapService'
import CommentHobby from '../components/CommentHobby'

export default {
  name: 'Detail',
  components: {
    MapService,
    CommentHobby

  },
  data () {
    return {
      data: {age: [0,0]},
      id: '',
      userId: '',
      joins: [],
      cnt: 0,
      flag: false,
      snackbar: false,
      ment: '포인트 충전을 위해 이동하시겠습니까?',
      vertical: true,
    }
  },
  mounted () {
    this.id = this.$route.params.id
    this.userId = this.$store.state.user_id
    this.getDetail()
    this.getJoinMember()
},
  methods: {
    move(){
      this.$router.push({name: 'user'})
    },
    yourPage(){
      console.log(this.data.user)
      if(this.data.user == this.$store.state.user_id){
        this.$router.push({name: 'user'})
      } else{
        this.$router.push({name: 'yourpage', params:{id:this.data.user}})
      }
    },
    getDetail: function () {
      const baseUrl = this.$store.state.baseUrl
      const apiUrl = baseUrl + 'boards/hobby/' + this.id
      this.$http.get(apiUrl)
      .then(res => {
        let startTime = res.data.startTime
        let startDay = res.data.startDay
        let endDay = res.data.endDay
        let created_at = res.data.created_at
        res.data.startTime = startTime.substring(0,2)+'시 '+startTime.substring(3,5)+'분'  
        res.data.startDay = startDay.substring(0,4)+'년 '+ startDay.substring(5,7)+'월 '+startDay.substring(8,10)+'일'
        res.data.endDay = endDay.substring(0,4)+'년 '+ endDay.substring(5,7)+'월 '+endDay.substring(8,10)+'일'
        res.data.created_at = created_at.substring(0,4)+'년 '+created_at.substring(5,7)+'월 '+created_at.substring(8,10)+'일' 

        res.data.fee = res.data.fee.toLocaleString()

        this.data = res.data 
      })
      .catch(err => {
        console.log(err)
      })
    },
    deleteDetail: function () {
      this.refundGroup()

      const baseUrl = this.$store.state.baseUrl
      const apiUrl = baseUrl + 'boards/hobby/' + this.id
      this.$http.delete(apiUrl)
        .then(res => {
            this.$router.go(-1)
        })
        .catch(err => {
            console.log(err)
        })
      },
      joinGroup: function () {
        let point = this.$store.state.user_point
        if(point >= 2000){
          const baseUrl = this.$store.state.baseUrl
          const apiUrl = baseUrl + 'boards/participantCheck/' + this.id + '/' + this.userId
          this.$http.post(apiUrl)
          .then(res => {
            this.pay()
  
            this.cnt += 1
            this.joins.unshift(res.data)
          })
          .catch(err => {
            console.log(err)
          })
        } else {
          alert("모임신청에 필요한 포인트가 부족합니다 !!")
          this.snackbar = true
        }

      },
      unjoinGroup: function (idx) {
        const baseUrl = this.$store.state.baseUrl
        const apiUrl = baseUrl + 'boards/participantCheck/' + this.id + '/' + this.userId
        this.$http.delete(apiUrl)
        .then(res => {
          this.refund()

          this.$router.go(-1)
        })
        .catch(err => {
          console.log(err)
        })
      },
      getJoinMember: function () {
        const baseUrl = this.$store.state.baseUrl
        const apiUrl = baseUrl + 'boards/participantCheckListByPost/' + this.id
        this.$http.get(apiUrl)
          .then(res => {
            this.cnt = res.data.user_group.length
            this.joins = res.data.user_group
            })
          .catch(err => {
            console.log(err)
          })
      },
      refundGroup: function () {
        for(let i of this.joins) {
          if(i.user_id !== this.data.user) {
            const baseUrl = this.$store.state.baseUrl
            const apiUrl = baseUrl + 'boards/refund/' + this.id +'/'+ i.user_id
            this.$http.post(apiUrl)
            .then(res => {
            })
            .catch(err => {
              console.log(err)
            })
          }
        }
      },
      refund: function () {
        const baseUrl = this.$store.state.baseUrl
        const apiUrl = baseUrl + 'boards/refund/' + this.id +'/'+ this.userId
        this.$http.post(apiUrl)
        .then(res => {
        })
        .catch(err => {
          console.log(err)
        })
      },
      pay: function () {
        const baseUrl = this.$store.state.baseUrl
        const apiUrl = baseUrl + 'boards/pay/' + this.id + '/'+ this.userId
        this.$http.post(apiUrl)
        .then(res => {
        })
        .catch(err => {
          console.log(err)
        })
      }
  }
}
</script>

<style lang="stylus">
.excard
  margin-bottom 48px

#leader
  height 50%

#member
  height 50%

#mapview
  height 300px
</style>
