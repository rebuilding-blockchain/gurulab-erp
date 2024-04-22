// 告诉Vue使用Vue Router
Vue.use(VueRouter);

// 定义一个Vue组件来展示和编辑工单模板
const TicketTemplateEdit = {
    template: `
    <section class="section">
        <div class="container">
            <div class="columns">
                <!-- 左侧列：State/State Transitions -->
                <div class="column is-half">
                    <article class="message is-primary">
                        <div class="message-header">
                            <p>Ticket Template: {{ ticketTemplate.name }}</p>
                        </div>
                        <div class="message-body">
                            <div class="field">
                                <label class="label">Name:</label>
                                <div class="control">
                                    <input class="input" v-model="ticketTemplate.name">
                                </div>
                            </div>

                            <div class="field">
                                <label class="label">Initial State:</label>
                                <div class="control">
                                    <div class="select">
                                        <select v-model="ticketTemplate.initial_state">
                                            <option v-for="state in Object.keys(ticketTemplate.state_transitions)" :key="state">
                                                {{ state }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div v-for="(transitions, state) in ticketTemplate.state_transitions" :key="state">
                                <div class="box">
                                    <h4 class="subtitle">State: {{ state }}</h4>
                                    <div v-for="(transition, nextState) in transitions" :key="nextState">
                                        <div class="field">
                                            <label class="label">Next State:</label>
                                            <div class="control">
                                                <input class="input" v-model="nextState">
                                            </div>
                                        </div>
                                        <div class="field">
                                            <label class="label">Action:</label>
                                            <div class="control">
                                                <input class="input" v-model="transition.action">
                                            </div>
                                        </div>
                                        <div class="field">
                                            <label class="label">Description:</label>
                                            <div class="control">
                                                <input class="input" v-model="transition.description">
                                            </div>
                                        </div>
                                    </div>
                                    <button class="button is-danger is-small" @click="deleteTransition(state, nextState)">Delete Transition</button>
                                </div>
                                <button class="button is-info is-small" @click="addTransition(state)">Add Transition</button>
                            </div>
                            <button class="button is-primary is-small" @click="addState">Add State</button>
                        </div>
                    </article>
                </div>

                <!-- 右侧列：Sub Template 相关内容编辑 -->
                <div class="column is-half">
                    <article class="message is-info">
                        <div class="message-header">
                            <p>Sub Template Configurations</p>
                        </div>
                        <div class="message-body">
                            <!-- 这里添加 Sub Template 的相关内容编辑界面 -->
                            <p>Sub Template editing interface will be here...</p>
                        </div>
                    </article>
                </div>
            </div>
        </div>
    </section>
    `,
    data() {
        return {
            editName: false,
            ticketTemplate: {
                name: '',
                initial_state: '',
                state_transitions: {}
            }
        };
    },
    mounted() {
        this.fetchTemplate();
    },
    methods: {
        toggleEditName(){
            console.log("toggle editName");
            this.editName = !this.editName;
        },
        fetchTemplate() {
            // Replace URL with your actual API URL
            axios.get(`/api/ticket_template/${this.$route.params.template_id}`)
                .then(response => {
                    this.ticketTemplate = response.data;
                })
                .catch(error => {
                    console.error('Error fetching the ticket template:', error);
                });
        },
        addState() {
            // Simple unique ID for example purposes
            let newState = 'State_' + Object.keys(this.ticketTemplate.state_transitions).length;
            this.$set(this.ticketTemplate.state_transitions, newState, {});
        },
        deleteState(state) {
            this.$delete(this.ticketTemplate.state_transitions, state);
        },
        addTransition(state) {
            let newTransition = 'NewState_' + Object.keys(this.ticketTemplate.state_transitions[state]).length;
            this.$set(this.ticketTemplate.state_transitions[state], newTransition, {action: '', description: ''});
        },
        deleteTransition(state, nextState) {
            this.$delete(this.ticketTemplate.state_transitions[state], nextState);
        },
        saveTemplate() {
            // Replace URL with your actual API URL
            axios.post(`/api/ticket_template/update/${this.ticketTemplate.template_id}`, this.ticketTemplate)
                .then(response => {
                    alert('Template updated successfully!');
                })
                .catch(error => {
                    console.error('Error updating the ticket template:', error);
                });
        }
    },
    beforeRouteEnter(to, from, next) {
         axios.get(`/api/ticket_template/${to.params.template_id}`)
             .then(response => {
                 console.log("Data received:", response.data);
                 next(vm => {
                     console.log("Inside next callback");  // 确认这条日志是否打印
                     vm.ticketTemplate = response.data;
                     console.log("Data set on vm:", vm.ticketTemplate);  // 检查数据是否被设置
                 });
             })
             .catch(error => {
                 console.error('Error loading the ticket template:', error);
             });
     }
};

// 设置Vue Router，定义路由
const router = new VueRouter({
    mode: 'history', // 使用HTML5 History模式
    routes: [
        {
            path: '/dashboard/ticket_template/:template_id',
            component: TicketTemplateEdit,
            props: true
        }
    ]
});

// 创建Vue实例并挂载到页面
new Vue({
    router
}).$mount('#ticket_template');