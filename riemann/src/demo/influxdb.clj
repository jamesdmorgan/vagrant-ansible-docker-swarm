(ns demo.influxdb)

; riemann already ships with support for influxdb, so we just need to require the function
(require '[riemann.influxdb :refer [influxdb]])
(require '[riemann.streams :refer [batch]])
(require '[riemann.test :refer [tap io]])

; here we set up an associative array that contains our configuration
; the (def) special form declares a variable; (def name value).
(def cfg
    {
        :host "influxdb"
        :port 8086
        :db "riemann-local"
        :username "root"
        :password "root"
        :version :0.9
    })

; Here we define a stream named "influx" that sends events to influx.
; We batch the events so that we send events when
;    a) we have 1000 events in our queue or
;    b) 2 seconds have passed since the last batch.
; This reduces our total number of network round-trips, and improves throughput.

(def influx
    (tap :influx
        (batch 1000 2
            (io (influxdb cfg))
        )
    )
)
