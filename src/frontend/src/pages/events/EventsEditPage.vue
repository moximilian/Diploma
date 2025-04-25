<template>
    <NestedPage title="Редактирование занятия">
        <template #page-content>
            <FormView v-if="entity" action="edit" :defaults="entity" displayName="events" >
                <template #form-bottom="{ entity }">
                    <BaseBtn v-if="!isStudent" @click="saveEvent(entity)">Сохранить</BaseBtn>
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
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
        groupName() {
            return this.$route.query.name ?? ''
        }
    },
    methods: {
        saveEvent(entity) {
            this.$api.events.update({ ...entity, id: this.eventId, repeat_id: this.entity.repeat_id }, res => {
                if (res.detail) return
                this.$router.replace(`/events/show/${res.id}`)
            })
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
        })
    }
}
</script>
