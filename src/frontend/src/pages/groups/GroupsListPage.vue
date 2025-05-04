<template>
    <NestedPage title="Группы">
        <template #page-header-right>
            <BaseBtn v-if="!isStudent" @click="$router.replace('/groups/new')"
                >Создать группу</BaseBtn
            >
        </template>
        <template #page-content>
            <div class="page-content-filter">
                <FilterForm :filterName="filterName" @changeFilters="changeFilters" />
                <TableView
                    ref="table"
                    :keys="keys"
                    displayName="groups"
                    :defaultFilters="defaultFilters"
                    :filters="filters"
                >
                    <template #last-item="{ row }" v-if="isStudent">
                        <TableCell>
                            <BaseBtn v-bind="buttonProps(row)" @click.stop="onGroupChange(row)" />
                        </TableCell>
                    </template>
                </TableView>
            </div>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            userId: null,
            filters: {
                wheres: [],
            },
        }
    },
    watch: {
        isStudent: {
            async handler() {
                await this.$refs.table.load()
            }
        },
    },
    computed: {
        keys() {
            return [
                { name: 'name' },
                { name: 'creator_id' },
                { name: 'description' },
                { name: 'is_open' },
                {
                    name: 'participant_count',
                    title: 'Кол-во участников',
                    format: row => [row.participant_count, row.max_participants_count].join('/'),
                },
                ...(this.isStudent ? [{ name: 'slot' }] : []),
            ]
        },
        filterName() {
            return this.isStudent ? 'groupsStudent' : 'groupsTeacher'
        },
        isStudent() {
            return this.$store.getters.isStudent
        },

        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: this.isStudent ? 'participant_id' : 'creator_id',
                            value: this.userId,
                        },
                        {
                            column: 'is_open',
                            value: true,
                        },
                    ],
                },
            }
        },
    },
    methods: {
        async changeFilters(wheres) {
            this.filters.wheres = wheres
            await this.$refs.table?.load()
        },
        buttonProps(row) {
            return {
                disabled:
                    row.is_participant || row.participant_count === row.max_participants_count,
                outline: true,
                value: this.buttonState(row),
            }
        },
        async onGroupChange(row) {
            const action = row.is_participant ? null : row.is_open ? 'enter' : 'send_request'
            if (action) {
                await this.$api.groups[action]({
                    id: row.id,
                })
                await this.$refs.table.load()
            }
        },
        buttonState(row) {
            return row.is_participant ? 'Учавствую' : row.is_open ? 'Вступить' : 'Отправить запрос'
        },
    },
    mounted() {
        this.userId = this.$route.query?.user_id ?? this.$ls.current_user ?? this.$store.state.id
    },
}
</script>
