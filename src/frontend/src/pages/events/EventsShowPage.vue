<template>
    <NestedPage title="Просмотр занятия">
        <template #page-content>
            <FormView
                v-if="entity"              
                displayName="events"
                action="show"
                :defaults="entity" >

                <template #form-bottom>
                    <BaseBtn :outline="true" @click="$router.push(`/home`)">Назад</BaseBtn>
                    <BaseBtn v-if="isGroupAdmin" @click="$router.push(`/events/edit/${entity.id}`)"
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
            eventId: null,
            entity: null,
            group: null
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
        groupName() {
            return this.$route.query.name ?? ''
        },
        isGroupAdmin() {
            return this.group && (this.$ls.current_user == this.group?.creator_id ?? false)
        },
    },
    created() {
        this.eventId = this.$route.params.id
        if (!this.eventId) {
            return console.error('Event ID is not given')
        }
        this.$api.events.one({ id: this.eventId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
            this.$api.groups.one({id: this.entity.group_id}, (res) => {
                this.group = res
            })
        })
    }
}
</script>
