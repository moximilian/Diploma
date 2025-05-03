<template>
    <NestedPage :title="entity?.name">
        <template #page-header-right>
            <div :class="{ selected: isSelected('about') }" @click="select('about')">О занятии</div>
            <div
                v-if="isGroupAdmin"
                :class="{ selected: isSelected('participants') }"
                @click="select('participants')"
            >
                Участники
            </div>
        </template>
        <template #page-content>
            <FormView
                v-if="entity && isSelected('about')"
                displayName="events"
                action="show"
                :defaults="entity"
            >
                <template #form-bottom>
                    <BaseBtn :outline="true" @click="$router.back()">Назад</BaseBtn>
                    <BaseBtn v-if="isGroupAdmin" @click="$router.push(`/events/edit/${eventId}`)"
                        >Изменить</BaseBtn
                    >
                </template>
            </FormView>
            <EventParticipantsPage v-if="isSelected('participants')" />
        </template>
    </NestedPage>
</template>
<script>
import EventParticipantsPage from './EventParticipantsPage.vue'
import TabsMixin from '@/pages/_help/TabsMixin'
export default {
    mixins: [TabsMixin],
    components: { EventParticipantsPage },
    data() {
        return {
            eventId: null,
            entity: null,
            group: null,
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
    async created() {
        this.eventId = this.$route.params.id
        if (!this.eventId) {
            return console.error('Event ID is not given')
        }
        this.select(this.selectedOption || 'about')
        const { body, ok } = await this.$api.events.one({ id: this.eventId })
        if (!ok) return console.error('Error during API call')
        this.entity = body
        const res = await this.$api.groups.one({ id: this.entity.group_id })
        this.group = res.body
    },
}
</script>
