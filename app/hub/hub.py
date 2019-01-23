from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0


class Hub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Hub, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        print"Inside packet_in_handler"

        pktin = ev.msg
        dpid = pktin.datapath.id
        ofp = pktin.datapath.ofproto
        ofp_parser = pktin.datapath.ofproto_parser

        print "DP id ",dpid, "OF_Proto ",ofp.OFP_VERSION


        inport = pktin.in_port
        bufferid = pktin.buffer_id
        len = pktin.total_len
        reason = pktin.reason
        data = pktin.data
        print ("inport ",inport,"bufferid ",bufferid,"packetlen ",len,"reason",reason,"data",data)

        'Flood all the packets'
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(datapath=pktin.datapath, buffer_id=bufferid, in_port=inport, actions=actions)
        pktin.datapath.send_msg(out)
