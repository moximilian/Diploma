<template>
    <NestedPage title="Редактирование занятия">
        <template #page-content>
            <FormView v-if="entity" action="edit" :defaults="entity" displayName="events">
                <template #form-bottom="{ entity }">
                    <BaseBtn v-if="!isStudent" @click="async () => await saveEvent(entity)"
                        >Сохранить</BaseBtn
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
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
        groupName() {
            return this.$route.query.name ?? ''
        },
    },
    methods: {
        async saveEvent(entity) {
            const { body, ok } = await this.$api.events.update({
                ...entity,
                id: this.eventId,
                repeat_id: this.entity.repeat_id,
            })
            if (!ok) return
            this.$router.replace(`/events/show/${body.id}`)
        },
    },
    async created() {
        this.eventId = this.$route.params.id
        if (!this.eventId) {
            return console.error('Event ID is not given')
        }
        const { body, ok } = await this.$api.events.one({ id: this.eventId })
        if (!ok) return console.error('Error during API call')
        this.entity = body
    },
}
</script>
