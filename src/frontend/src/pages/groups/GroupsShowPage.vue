<template>
    <NestedPage :title="entity?.name">
        <template #page-header-right>
            <div :class="{ selected: isSelected('about') }" @click="select('about')">О группе</div>
            <div :class="{ selected: isSelected('participants') }" @click="select('participants')">
                Участники
            </div>
            <div
                v-if="!entity?.is_open ?? false"
                :class="{ selected: isSelected('enter_requests') }"
                @click="select('enter_requests')"
            >
                Заявки на вступление
            </div>
            <BaseBtn :disabled="true">Добавить занятие</BaseBtn>
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
                    <BaseBtn @click="$router.push(`/groups/edit/${groupId}`)">Изменить</BaseBtn>
                </template>
            </FormView>
            <ParticipantListPage v-if="isSelected('participants')" :groupId="groupId" />
            <EnterRequestsInListPage v-if="isSelected('enter_requests')" :groupId="groupId" />
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
