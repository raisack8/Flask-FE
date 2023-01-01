var app = new Vue({
    el:'#app',
    data:{
        toggle: true
    },
    methods:{
        toggleBtn: function(){
            this.toggle == true ? this.toggle = false : this.toggle = true
        }
    }
})