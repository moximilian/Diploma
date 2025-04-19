<template>
    <span class="header-container page">
        <div class="logo" style="width: 64px; height: 64px"></div>
        <div class="header">
            <div class="flex-container-row">
                <BaseBtn
                    :outline="isSelected('home')"
                    :inactive="!isSelected('home')"
                    :special="true"
                    class
                    @click="toHomePage"
                >
                    Расписание
                </BaseBtn>
                <BaseBtn
                    :outline="isSelected('groups')"
                    :inactive="!isSelected('groups')"
                    :special="true"
                    @click="toGroups"
                >
                    Группы
                </BaseBtn>
            </div>
        </div>
        <div @mouseenter="toggleCard" @mouseleave="() => (isTooltipOpen = false)" ref="triggerElem">
            <PhotoField :src="imageSrc" className="profile-pic" />
        </div>
        <teleport to="body">
            <div
                class="card"
                ref="movableElem"
                @mouseenter="toggleCard"
                @mouseleave="() => (isTooltipOpen = false)"
            >
                <div class="card-wrapper" v-if="isTooltipOpen">
                    <div class="naming">
                        <PhotoField :src="imageSrc" className="profile-pic" />
                        <h4>{{ currentUser?.name }} {{ currentUser?.surname }}</h4>
                        <span class="gray">{{ currentUser?.login }}</span>
                    </div>
                    <div class="line"></div>
                    <div class="links">
                        <div class="link">
                            <router-link :to="`/user/edit/${currentUserId}?tab=personalInfo`">
                                Профиль
                            </router-link>
                        </div>
                        <div class="link" v-if="!currentUser?.is_external_auth">
                            <router-link :to="`/user/edit/${currentUserId}?tab=settings`">
                                Настройки
                            </router-link>
                        </div>
                        <div class="link">
                            <a> FAQ </a>
                        </div>
                    </div>
                    <div class="line"></div>
                    <div class="links">
                        <div class="link">
                            <a @click="logout"> Выйти </a>
                        </div>
                        <!-- <div class="link">
                            <router-link :to="`/user/edit/${currentUserId}`">
                                Удалить аккаунт
                            </router-link>
                        </div> -->
                    </div>
                </div>
            </div>
        </teleport>
    </span>
</template>
<style>
.card {
    position: absolute;
    visibility: hidden;
    background-color: white;
    width: 203px !important;
    border-radius: 8px;
    box-shadow: 3px 3px 30px rgba(0, 0, 0, 0.1);
}
.card-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    margin-bottom: 10px;
}
.card-wrapper .naming {
    display: flex;
    padding-left: 8px;
    padding-right: 8px;
    flex-direction: column;
    align-items: center;
}
.line {
    border-bottom: 1px solid var(--gray-color);
    width: 90%;
}
.links {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    text-align: left;
}
.links .link,
.links .link a,
.links a {
    color: black;
    padding-left: 16px;
    padding-top: 8px;
    padding-bottom: 8px;
    cursor: pointer;
}
.links div:hover {
    background-color: var(--light-gray-color);
}
.gray {
    color: var(--gray-color);
}
</style>
<script>
import SelectPositionMixin from '../help/SelectPositionMixin'
export default {
    mixins: [SelectPositionMixin],
    data() {
        return {
            currentUser: null,
            isTooltipOpen: false,
        }
    },
    watch: {
        currentUserId() {
            this.currentUserId && this.getCurrentUser()
        },
    },
    methods: {
        toggleCard() {
            this.isTooltipOpen = !this.isTooltipOpen
            this.setPosition(true, false, 155)
        },

        isSelected(page) {
            return this.$route?.fullPath.search(page) === 1
        },
        toHomePage() {
            this.$router.push('/home?tab=today')
        },
        toGroups() {
            this.$router.push(`/groups/list?user_id=${this.currentUserId}`)
        },
        logout() {
            this.$api.auth.logout({ access_token: this.$ls.token }, () => {
                this.$ls.token = null
                this.$ls.current_user = null
                this.$router.push('/auth/login')
            })
        },
        getCurrentUser() {
            this.$api.users.one({ id: this.$ls.current_user }, res => {
                this.currentUser = res
                if (res?.photo_id || this.imageSrc === null) this.fetchImage(res.photo_id)
                this.$store.commit('setRole', res.role_name)
            }) ?? ''
        },
        fetchImage(id) {
            this.$api.images.get({ id }, res => {
                this.$store.commit('setPhoto', res)
            })
        },
    },
    computed: {
        currentUserId() {
            return this.currentUser?.id ?? this.$ls.current_user
        },
        imageSrc() {
            return this.$store.state.photo64 ?? null
        },
    },
    created() {
        if (this.currentUser === null) this.getCurrentUser()
    },
}
</script>
