(ns demo.util)

(defn is-not-nan?
     [event]
     (or
       (nil? (:metric event))
       (not (Double/isNaN (:metric event)))))
