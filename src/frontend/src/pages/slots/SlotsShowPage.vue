<template>
    <NestedPage title="Просмотр слота">
        <template #page-content>
            <FormView v-if="entity" displayName="slots" action="show" :defaults="entity">
                <template #form-bottom>
                    <BaseBtn :outline="true" @click="$router.push(`/home`)">Назад</BaseBtn>
                    <BaseBtn v-if="isStudent && entity.is_participant" @click="leaveSlot()"
                        >Покинуть</BaseBtn
                    >
                    <BaseBtn v-else-if="isStudent" @click="enterSlot()"
                        >Занять место</BaseBtn
                    >
                    <BaseBtn v-if="isSlotAdmin" @click="$router.push(`/slots/edit/${slotId}`)"
                        >Изменить</BaseBtn
                    >
                </template>
            </FormView>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            slotId: null,
            entity: null,
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
        isSlotAdmin() {
            return !this.isStudent && this.entity.creator_id === this.$ls.current_user
        },
    },
    methods: {
        enterSlot() {
            this.$api.slots.enter({ id: this.slotId }, () => {
                this.$router.go(this.$router.currentRoute)
            })
        },
        leaveSlot() {
            this.$api.slots.leave({ id: this.slotId }, () => {
                this.$router.go(this.$router.currentRoute)
            })
        },
    },
    created() {
        this.slotId = this.$route.params.id
        if (!this.slotId) {
            return console.error('slot ID is not given')
        }
        this.$api.slots.one({ id: this.slotId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
