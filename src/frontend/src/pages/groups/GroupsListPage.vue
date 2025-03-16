<template>
    <div class="page-container">
        <div class="page user">
            <div class="page-header-wrapper">
                <div class="page-title">Группы</div>
                <div class="page-right">
                    <BaseBtn @click="$router.replace('/groups/new')">Создать группу</BaseBtn>
                </div>
            </div>

            <div class="page-content-filter">
                <FilterForm filterName="groups" @changeFilters="changeFilters" />
                <TableView
                    ref="table"
                    :keys="keys"
                    displayName="groups"
                    :defaultFilters="defaultFilters"
                    :filters="filters"
                />
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            keys: [
                { name: 'name' },
                { name: 'creator_id' },
                { name: 'description' },
                { name: 'is_open' },
                { name: 'max_participants_count' },
            ],
            userId: null,
            filters: {
                wheres: [],
            },
        }
    },
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column:
                                this.userId === this.$ls.current_user
                                    ? 'creator_id'
                                    : 'participant_id',
                            value: this.userId,
                        },
                        {
                            column:'is_open',
                            value: true,
                        },
                    ],
                },
            }
        },
    },
    methods: {
        changeFilters(wheres) {
            this.filters.wheres = wheres
            this.$refs.table.load()
        },
    },
    created() {
        this.userId = this.$route.query?.user_id ?? this.$ls.current_user
    },
}
</script>
