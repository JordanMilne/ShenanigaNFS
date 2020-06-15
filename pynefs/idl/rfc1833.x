/*
 * rpcb_prot.x
 * rpcbind protocol, versions 3 and 4, in RPC Language
 */

/*
 * rpcbind address for TCP/UDP
 */
const RPCB_PORT = 111;

/*
 * A mapping of (program, version, network ID) to address
 *
 * The network identifier  (r_netid):
 * This is a string that represents a local identification for a
 * network. This is defined by a system administrator based on local
 * conventions, and cannot be depended on to have the same value on
 * every system.
 */
struct rpcb {
 unsigned long r_prog;    /* program number */
 unsigned long r_vers;    /* version number */
 string r_netid<>;        /* network id */
 string r_addr<>;         /* universal address */
 string r_owner<>;        /* owner of this service */
};

struct rp__list {
 rpcb rpcb_map;
 rp__list *rpcb_next;
};

typedef rp__list rpcblist;

/*
 * Arguments of remote calls
 */
struct rpcb_rmtcallargs {
 unsigned long prog;        /* program number */
 unsigned long vers;        /* version number */
 unsigned long proc;        /* procedure number */
 opaque args<>;             /* argument */
};


/*
 * Results of the remote call
 */
struct rpcb_rmtcallres {
 string addr<>;            /* remote universal address */
 opaque results<>;         /* result */
};


/*
 * rpcb_entry contains a merged address of a service on a particular
 * transport, plus associated netconfig information.  A list of
 * rpcb_entry items is returned by RPCBPROC_GETADDRLIST.  The meanings
 * and values used for the r_nc_* fields are given below.
 *
 * The network identifier  (r_nc_netid):

 *   This is a string that represents a local identification for a
 *   network.  This is defined by a system administrator based on
 *   local conventions, and cannot be depended on to have the same
 *   value on every system.
 *
 * Transport semantics (r_nc_semantics):
 *  This represents the type of transport, and has the following values:
 *     NC_TPI_CLTS     (1)      Connectionless
 *     NC_TPI_COTS     (2)      Connection oriented
 *     NC_TPI_COTS_ORD (3)      Connection oriented with graceful close
 *     NC_TPI_RAW      (4)      Raw transport
 *
 * Protocol family (r_nc_protofmly):
 *   This identifies the family to which the protocol belongs.  The
 *   following values are defined:
 *     NC_NOPROTOFMLY   "-"
 *     NC_LOOPBACK      "loopback"
 *     NC_INET          "inet"
 *     NC_IMPLINK       "implink"
 *     NC_PUP           "pup"
 *     NC_CHAOS         "chaos"
 *     NC_NS            "ns"
 *     NC_NBS           "nbs"
 *     NC_ECMA          "ecma"
 *     NC_DATAKIT       "datakit"
 *     NC_CCITT         "ccitt"
 *     NC_SNA           "sna"
 *     NC_DECNET        "decnet"
 *     NC_DLI           "dli"
 *     NC_LAT           "lat"
 *     NC_HYLINK        "hylink"
 *     NC_APPLETALK     "appletalk"
 *     NC_NIT           "nit"
 *     NC_IEEE802       "ieee802"
 *     NC_OSI           "osi"
 *     NC_X25           "x25"
 *     NC_OSINET        "osinet"
 *     NC_GOSIP         "gosip"
 *
 * Protocol name (r_nc_proto):
 *   This identifies a protocol within a family.  The following are
 *   currently defined:
 *      NC_NOPROTO      "-"
 *      NC_TCP          "tcp"
 *      NC_UDP          "udp"
 *      NC_ICMP         "icmp"
 */
struct rpcb_entry {
 string          r_maddr<>;            /* merged address of service */
 string          r_nc_netid<>;         /* netid field */
 unsigned long   r_nc_semantics;       /* semantics of transport */
 string          r_nc_protofmly<>;     /* protocol family */
 string          r_nc_proto<>;         /* protocol name */
};

/*
 * A list of addresses supported by a service.
 */
struct rpcb_entry_list {
 rpcb_entry rpcb_entry_map;
 rpcb_entry_list *rpcb_entry_next;
};

/*typedef rpcb_entry_list *rpcb_entry_list_ptr;*/

/*
 * rpcbind statistics
 */

const rpcb_highproc_2 = 5;
const rpcb_highproc_3 = 8;
const rpcb_highproc_4 = 12;

const RPCBSTAT_HIGHPROC = 13; /* # of procs in rpcbind V4 plus one */
const RPCBVERS_STAT     = 3; /* provide only for rpcbind V2, V3 and V4 */
const RPCBVERS_4_STAT   = 2;
const RPCBVERS_3_STAT   = 1;
const RPCBVERS_2_STAT   = 0;

/* Link list of all the stats about getport and getaddr */
struct rpcbs_addrlist {
 unsigned long prog;
 unsigned long vers;
 int success;
 int failure;
 string netid<>;
 rpcbs_addrlist *next;
};

/* Link list of all the stats about rmtcall */
struct rpcbs_rmtcalllist {
 unsigned long prog;
 unsigned long vers;
 unsigned long proc;
 int success;
 int failure;
 int indirect;    /* whether callit or indirect */
 string netid<>;
 rpcbs_rmtcalllist *next;
};

typedef int rpcbs_proc[RPCBSTAT_HIGHPROC];
/*
typedef rpcbs_addrlist *rpcbs_addrlist_ptr;
typedef rpcbs_rmtcalllist *rpcbs_rmtcalllist_ptr;
*/

struct rpcb_stat {
 rpcbs_proc              info;
 int                     setinfo;
 int                     unsetinfo;
 rpcbs_addrlist *      addrinfo;
 rpcbs_rmtcalllist *   rmtinfo;
};

/*
 * One rpcb_stat structure is returned for each version of rpcbind
 * being monitored.
 */

typedef rpcb_stat rpcb_stat_byvers[RPCBVERS_STAT];

/*
 * netbuf structure, used to store the transport specific form of
 * a universal transport address.
 */
struct netbuf {
 unsigned int maxlen;
 opaque buf<>;
};


/*
 * rpcbind procedures
 */
program RPCBPROG {
 version RPCBVERS {
     bool
     RPCBPROC_SET(rpcb) = 1;

     bool
     RPCBPROC_UNSET(rpcb) = 2;

     string
     RPCBPROC_GETADDR(rpcb) = 3;

     rpcblist*
     RPCBPROC_DUMP(void) = 4;

     rpcb_rmtcallres
     RPCBPROC_CALLIT(rpcb_rmtcallargs) = 5;

     unsigned int
     RPCBPROC_GETTIME(void) = 6;

     netbuf
     RPCBPROC_UADDR2TADDR(string) = 7;

     string
     RPCBPROC_TADDR2UADDR(netbuf) = 8;
 } = 3;

 version RPCBVERS4 {
     bool
     RPCBPROC_SET(rpcb) = 1;

     bool
     RPCBPROC_UNSET(rpcb) = 2;

     string
     RPCBPROC_GETADDR(rpcb) = 3;

     rpcblist*
     RPCBPROC_DUMP(void) = 4;

     /*
      * NOTE: RPCBPROC_BCAST has the same functionality as CALLIT;
      * the new name is intended to indicate that this
      * procedure should be used for broadcast RPC, and
      * RPCBPROC_INDIRECT should be used for indirect calls.
      */
     rpcb_rmtcallres
     RPCBPROC_BCAST(rpcb_rmtcallargs) = 5;

     unsigned int
     RPCBPROC_GETTIME(void) = 6;

     netbuf
     RPCBPROC_UADDR2TADDR(string) = 7;

     string
     RPCBPROC_TADDR2UADDR(netbuf) = 8;

     string
     RPCBPROC_GETVERSADDR(rpcb) = 9;

     rpcb_rmtcallres
     RPCBPROC_INDIRECT(rpcb_rmtcallargs) = 10;

     rpcb_entry_list*
     RPCBPROC_GETADDRLIST(rpcb) = 11;

     rpcb_stat_byvers
     RPCBPROC_GETSTAT(void) = 12;
 } = 4;
} = 100000;
