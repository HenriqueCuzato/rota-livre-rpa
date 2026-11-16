import { sqliteTable, text, real, integer } from 'drizzle-orm/sqlite-core';
export const occurrences = sqliteTable('occurrences', {
 id:text('id').primaryKey(),title:text('title').notNull(),category:text('category').notNull(),address:text('address').notNull(),description:text('description').notNull(),lat:real('lat').notNull(),lng:real('lng').notNull(),status:text('status').notNull(),created:text('created').notNull(),updated:text('updated').notNull(),photo:text('photo'),demo:integer('demo').notNull().default(0)
});
