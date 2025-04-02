<template>
    <NestedPage :title="entity?.name">
        <template #page-header-right>
            <div :class="{ selected: isSelected('about') }" @click="select('about')">О группе</div>
            <div
                v-if="entity?.is_participant || isGroupAdmin"
                :class="{ selected: isSelected('participants') }"
                @click="select('participants')"
            >
                Участники
            </div>
            <div
                v-if="(!entity?.is_open ?? false) && isGroupAdmin"
                :class="{ selected: isSelected('enter_requests') }"
                @click="select('enter_requests')"
            >
                Заявки на вступление
            </div>
            <BaseBtn v-if="isGroupAdmin" :disabled="true" :outline="true">Добавить занятие</BaseBtn>
        </template>
        <template #page-content>
            <FormView
                v-if="entity && isSelected('about')"
                displayName="groups"
                action="show"
                :defaults="entity"
            >
                <template #form-bottom>
                    <BaseBtn :outline="true" @click="$router.push(`/groups/list`)">Назад</BaseBtn>
                    <BaseBtn
                        v-if="isStudent && entity?.is_participant"
                        @click="leaveGroup(entity.id)"
                        >Покинуть</BaseBtn
                    >
                    <BaseBtn v-if="isGroupAdmin" @click="$router.push(`/groups/edit/${groupId}`)"
                        >Изменить</BaseBtn
                    >
                </template>
            </FormView>
            <ParticipantListPage
                v-if="isSelected('participants') && (entity?.is_participant || isGroupAdmin)"
                :groupId="groupId"
                :entity="entity"
            />
            <EnterRequestsInListPage
                v-if="isSelected('enter_requests') && isGroupAdmin"
                :groupId="groupId"
                :entity="entity"
            />
        </template>
    </NestedPage>
</template>
<script>
import TabsMixin from '@/pages/_help/TabsMixin'
import ParticipantListPage from '../participants/ParticipantListPage'
import EnterRequestsInListPage from '../enter_requests/EnterRequestsInListPage'

export default {
    mixins: [TabsMixin],
    components: { ParticipantListPage, EnterRequestsInListPage },
    data() {
        return {
            groupId: null,
            entity: null,

            selectedOption: 'about',
        }
    },
    methods: {
        leaveGroup(id) {
            this.$api.groups.leave({ id }, () => {
                this.$router.push(`/groups/list`)
            })
        },
    },
    computed: {
        isGroupAdmin() {
            return this.$ls.current_user == this.entity?.creator_id ?? false
        },
        isStudent() {
            return this.$store.getters.isStudent
        },
    },
    created() {
        this.groupId = this.$route.params.id
        if (!this.groupId) {
            return console.error('User ID is not given')
        }
        this.$api.groups.one({ id: this.groupId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
