(include "riemann.config")
(require '[demo.util :refer [is-not-nan?]])

; Riemann offers two helpful functions for unit testing.
; The first is `tap`. The tap function records all the events that
; pass through it.
; You can use it like this:
;
;  (streams
;     (where* is-nan?
;        (tap :nan)))
;
; This sets up a tap called :nan inside our where stream. We can use that to
; check that an event with a metric value of NaN is matched by the is-nan?
; function.
;
; The other useful function is `io`. The io function swallows events and throws them in the bit-bucket
; when riemann is running in test mode.
; eg.
;
;  (streams
;     (io influx))
;
; will *not* call the influx stream when running unit tests, this is useful to prevent spamming
; slack and pagerduty while testing. When riemann is not running in test mode, the io function
; just passes events to its children.

(tests
      ;; deftest starts a new unit test.
       (deftest true-is-true

          ; the `is` function performs an assertion.
          ; in this case, we're just testing that true == true.
          (is (= true true)))

       (deftest events-are-sent-to-influx

         ; The inject function puts an list of events into the riemann queue
         ; and returns a map of all the taps and the events that
         ; reached them.
         ; eg. using the config from the top of this file, if we injected
         ;
         ; [
         ;   {:service "myservice" :metric Double/NaN}
         ;   {:service "myservice" :metric 10.0 }
         ; ]
         ;
         ; the return value would be
         ; {
         ;    :nan [{:service "myservice" :metric Double/NaN}]
         ; }
         ;
         ; The get function takes a key and a map and returns the matching
         ; value, if any.
         ; eg. If mymap contains the above map, then
         ;
         ; (get mymap :nan)
         ;
         ; returns the list [{:service "myservice" :metric Double/NaN}]


         ; e is just an event to play with
         (def e {
                  :service "myservice"
                  :metric 23
                  :host "localhost"
                  :state "ok"
                  :ttl 10
                  :time 0
                  })

          ; Here we inject a single event into riemann and check that it ends up in a tap
          ; named influx.
          ;
          ; To make the test pass, update the influx stream in src/made/influxdb.clj
          ; and add the io and tap function calls.
          (is (=
               (get (inject! [e]) :influx)
               [e]
          )))

        ; Complete the definition of this test and make it pass.
        ; Your injected event should have a metric of Double/NaN
        (deftest nan-metrics-do-not-arrive-in-influx
          (def e {
                  :service "myservice"
                  :metric Double/NaN
                  })

          ; Here we inject a single event into riemann and check that it ends up in a tap
          ; named influx.
          ;
          ; To make the test pass, update the influx stream in src/made/influxdb.clj
          ; and add the io and tap function calls.
          (is (not (=
               (get (inject! [e]) :influx)
               [e])
          )))
)
