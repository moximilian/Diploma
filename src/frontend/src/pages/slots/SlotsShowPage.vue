<template>
    <NestedPage title="Просмотр слота">
        <template #page-header-right>
            <div :class="{ selected: isSelected('about') }" @click="select('about')">О слоте</div>
            <div
                v-if="isSlotAdmin"
                :class="{ selected: isSelected('participants') }"
                @click="select('participants')"
            >
                Участники
            </div>
        </template>
        <template #page-content>
            <FormView
                v-if="entity && isSelected('about')"
                displayName="slots"
                action="show"
                :defaults="entity"
            >
                <template #form-bottom>
                    <BaseBtn :outline="true" @click="$router.back()">Назад</BaseBtn>
                    <BaseBtn v-if="isStudent && entity.is_participant" @click="leaveSlot()"
                        >Покинуть</BaseBtn
                    >
                    <BaseBtn
                        v-else-if="
                            isStudent && entity.participants_count < entity.max_participants_count
                        "
                        @click="enterSlot()"
                        >Занять место</BaseBtn
                    >
                    <BaseBtn v-if="isSlotAdmin" @click="$router.push(`/slots/edit/${slotId}`)"
                        >Изменить</BaseBtn
                    >
                </template>
            </FormView>
            <SlotsParticipantPage v-if="isSelected('participants')" />
        </template>
    </NestedPage>
</template>
<script>
import SlotsParticipantPage from './SlotsParticipantPage.vue'
import TabsMixin from '../_help/TabsMixin'
export default {
    mixins: [TabsMixin],
    components: { SlotsParticipantPage },
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
            return (
                !this.isStudent && this.entity && this.entity.creator_id === this.$ls.current_user
            )
        },
    },
    methods: {
        async enterSlot() {
            await this.$api.slots.enter({ id: this.slotId })
            this.$router.go(this.$router.currentRoute)
        },
        async leaveSlot() {
            await this.$api.slots.leave({ id: this.slotId })
            this.$router.go(this.$router.currentRoute)
        },
    },
    async created() {
        this.slotId = this.$route.params.id
        if (!this.slotId) {
            return console.error('slot ID is not given')
        }
        this.select(this.selectedOption || 'about')
        const { body, ok } = await this.$api.slots.one({ id: this.slotId })
        if (!ok) return console.error('Error during API call')
        this.entity = body
    },
}
</script>
