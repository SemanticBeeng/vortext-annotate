(ns spa.db.projects
  (:refer-clojure :exclude [get])
  (:require [spa.db.schema :refer [db-spec]]
            [clojure.java.io :as io]
            [yesql.core :refer [defquery defqueries]]
            [clojure.java.jdbc :as jdbc]))

(defqueries "sql/projects.sql")

(defn has?
  [user-id project-id]
  (:exists (first (has-project? db-spec user-id project-id))))

(defn get
  [project-id]
  (first (get-project db-spec project-id)))

(defn for-user
  [user-id]
  (select-projects-by-user db-spec user-id))

(defn create!
  [user-id title description]
  (create-project<! db-spec title description user-id))

(defn edit!
  [id title description]
  (edit-project! db-spec title description id))