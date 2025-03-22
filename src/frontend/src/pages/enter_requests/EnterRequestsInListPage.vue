<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="enter_requests"
        :defaultFilters="defaultFilters"
        :filters="defaultFilters"
        :isClickable="false"
    >
        <template #first-item="{ row }">
            <TableCellCheckBox @clickCheckBox="isChecked => onCheckboxChecked(isChecked, row)" />
        </template>
        <template #after-table="{ rows }">
            <BaseBtn
                v-if="rows.length > 0"
                :outline="true"
                value="Отклонить"
                @click="changeUserStatus('revoke')"
            />
            <BaseBtn v-if="rows.length > 0" value="Принять" @click="changeUserStatus('accept')" />
        </template>
    </TableView>
</template>

<script>
export default {
    // Здесь клик в таблицу должен проваливаться в карточку пользователя
    props: {
        groupId: { type: String, default: () => '' },
    },
    data() {
        return {
            keys: [
                {
                    name: 'fio',
                    title: 'ФИО',
                },
                { name: 'login', title: 'Логин' },
                { name: 'datetime' },
                { name: 'is_approved' },
            ],
            selectedIds: new Map(),
        }
    },
    methods: {
        onCheckboxChecked(isChecked, { id }) {
            isChecked ? this.selectedIds.set(id, true) : this.selectedIds.delete(id, true)
        },
        changeUserStatus(status) {
            Array.from(this.selectedIds).map(item => {
                this.$api.enter_requests[status]({ id: item[0] })
            })
            this.$refs.table.load()
        },
    },
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'group_id',
                            value: this.groupId,
                        },
                    ],
                },
            }
        },
    },
}
</script>
